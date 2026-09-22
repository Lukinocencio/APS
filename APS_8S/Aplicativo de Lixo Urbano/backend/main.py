from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from datetime import datetime, timezone, timedelta
import uuid
import os
import shutil

DB_PATH = "pontos.db"
PASTA_FOTOS = "fotos"
os.makedirs(PASTA_FOTOS, exist_ok=True)

VOTOS_PARA_VALIDAR = 10  # quantidade de votos até decidir o ponto

app = FastAPI(title="API - Pontos de Lixo Urbano")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Deixa as fotos acessíveis via URL, ex: http://IP:8000/fotos/nome-do-arquivo.jpg
app.mount("/fotos", StaticFiles(directory=PASTA_FOTOS), name="fotos")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------- Schemas (formato dos dados que entram/saem da API) ----------

class PontoCreate(BaseModel):
    tipo: str  # lixeira | descarte_irregular | bueiro_entupido
    latitude: float
    longitude: float
    descricao: Optional[str] = None
    reportado_por: Optional[str] = "anonimo"


class VotoCreate(BaseModel):
    voto: str  # verdadeiro | falso


class Foto(BaseModel):
    id: str
    ponto_id: str
    url: str
    criado_em: str


class Ponto(BaseModel):
    id: str
    tipo: str
    latitude: float
    longitude: float
    status: str  # pendente | validado | invalidado
    descricao: Optional[str] = None
    reportado_por: Optional[str] = None
    criado_em: str
    atualizado_em: str
    expira_em: str
    votos_verdadeiro: int
    votos_falso: int
    fotos: List[Foto] = []


# ---------- Funções auxiliares ----------

def linha_para_ponto(conn, row: sqlite3.Row) -> dict:
    fotos_rows = conn.execute(
        "SELECT * FROM fotos WHERE ponto_id = ? ORDER BY criado_em", (row["id"],)
    ).fetchall()
    fotos = [
        {
            "id": f["id"],
            "ponto_id": f["ponto_id"],
            "url": f"/fotos/{os.path.basename(f['caminho_arquivo'])}",
            "criado_em": f["criado_em"],
        }
        for f in fotos_rows
    ]

    votos_verdadeiro = conn.execute(
        "SELECT COUNT(*) as total FROM votos WHERE ponto_id = ? AND voto = 'verdadeiro'",
        (row["id"],),
    ).fetchone()["total"]
    votos_falso = conn.execute(
        "SELECT COUNT(*) as total FROM votos WHERE ponto_id = ? AND voto = 'falso'",
        (row["id"],),
    ).fetchone()["total"]

    return {
        "id": row["id"],
        "tipo": row["tipo"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "status": row["status"],
        "descricao": row["descricao"],
        "reportado_por": row["reportado_por"],
        "criado_em": row["criado_em"],
        "atualizado_em": row["atualizado_em"],
        "expira_em": row["expira_em"],
        "votos_verdadeiro": votos_verdadeiro,
        "votos_falso": votos_falso,
        "fotos": fotos,
    }


# ---------- Endpoints ----------

@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API de pontos de lixo urbano no ar"}


@app.get("/pontos", response_model=List[Ponto])
def listar_pontos():
    """Só retorna pontos que ainda não passaram das 24h."""
    conn = get_db()
    agora = datetime.now(timezone.utc).isoformat()
    rows = conn.execute(
        "SELECT * FROM pontos WHERE expira_em > ? ORDER BY criado_em DESC", (agora,)
    ).fetchall()
    resultado = [linha_para_ponto(conn, r) for r in rows]
    conn.close()
    return resultado


@app.post("/pontos", response_model=Ponto)
def criar_ponto(ponto: PontoCreate):
    conn = get_db()
    novo_id = str(uuid.uuid4())
    agora = datetime.now(timezone.utc)
    expira = agora + timedelta(hours=24)

    conn.execute(
        """INSERT INTO pontos
           (id, tipo, latitude, longitude, status, descricao, reportado_por,
            criado_em, atualizado_em, expira_em)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            novo_id,
            ponto.tipo,
            ponto.latitude,
            ponto.longitude,
            "pendente",
            ponto.descricao,
            ponto.reportado_por,
            agora.isoformat(),
            agora.isoformat(),
            expira.isoformat(),
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM pontos WHERE id = ?", (novo_id,)).fetchone()
    resultado = linha_para_ponto(conn, row)
    conn.close()
    return resultado


@app.post("/pontos/{ponto_id}/fotos", response_model=Foto)
async def enviar_foto(ponto_id: str, arquivo: UploadFile = File(...)):
    conn = get_db()
    ponto = conn.execute("SELECT * FROM pontos WHERE id = ?", (ponto_id,)).fetchone()
    if ponto is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Ponto não encontrado")

    extensao = os.path.splitext(arquivo.filename)[1] or ".jpg"
    nome_arquivo = f"{uuid.uuid4()}{extensao}"
    caminho = os.path.join(PASTA_FOTOS, nome_arquivo)

    with open(caminho, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    foto_id = str(uuid.uuid4())
    agora = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO fotos (id, ponto_id, caminho_arquivo, criado_em) VALUES (?, ?, ?, ?)",
        (foto_id, ponto_id, caminho, agora),
    )
    conn.commit()
    conn.close()

    return {
        "id": foto_id,
        "ponto_id": ponto_id,
        "url": f"/fotos/{nome_arquivo}",
        "criado_em": agora,
    }


@app.post("/pontos/{ponto_id}/votos", response_model=Ponto)
def votar(ponto_id: str, voto: VotoCreate):
    if voto.voto not in ("verdadeiro", "falso"):
        raise HTTPException(status_code=400, detail="Voto deve ser 'verdadeiro' ou 'falso'")

    conn = get_db()
    ponto = conn.execute("SELECT * FROM pontos WHERE id = ?", (ponto_id,)).fetchone()
    if ponto is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Ponto não encontrado")

    if ponto["status"] != "pendente":
        conn.close()
        raise HTTPException(status_code=400, detail="Este ponto já foi validado ou invalidado")

    voto_id = str(uuid.uuid4())
    agora = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO votos (id, ponto_id, voto, criado_em) VALUES (?, ?, ?, ?)",
        (voto_id, ponto_id, voto.voto, agora),
    )
    conn.commit()

    total_votos = conn.execute(
        "SELECT COUNT(*) as total FROM votos WHERE ponto_id = ?", (ponto_id,)
    ).fetchone()["total"]

    # Assim que bater o número definido de votos, o ponto é decidido automaticamente
    if total_votos >= VOTOS_PARA_VALIDAR:
        votos_verdadeiro = conn.execute(
            "SELECT COUNT(*) as total FROM votos WHERE ponto_id = ? AND voto = 'verdadeiro'",
            (ponto_id,),
        ).fetchone()["total"]
        votos_falso = total_votos - votos_verdadeiro
        novo_status = "validado" if votos_verdadeiro > votos_falso else "invalidado"
        conn.execute(
            "UPDATE pontos SET status = ?, atualizado_em = ? WHERE id = ?",
            (novo_status, agora, ponto_id),
        )
        conn.commit()

    row = conn.execute("SELECT * FROM pontos WHERE id = ?", (ponto_id,)).fetchone()
    resultado = linha_para_ponto(conn, row)
    conn.close()
    return resultado


@app.delete("/pontos/{ponto_id}")
def deletar_ponto(ponto_id: str):
    conn = get_db()
    conn.execute("DELETE FROM fotos WHERE ponto_id = ?", (ponto_id,))
    conn.execute("DELETE FROM votos WHERE ponto_id = ?", (ponto_id,))
    conn.execute("DELETE FROM pontos WHERE id = ?", (ponto_id,))
    conn.commit()
    conn.close()
    return {"status": "removido"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)