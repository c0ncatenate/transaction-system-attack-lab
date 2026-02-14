from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional
import jwt

JWT_SECRET = "lab-secret-key"
JWT_ALG = "HS256"

app = FastAPI(title="accounts-service")


class Account(BaseModel):
    id: int
    owner_user_id: int
    balance: float


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float


# In-memory accounts store for the lab.
# NOTE: Deliberately simple and vulnerable for educational purposes.
ACCOUNTS: Dict[int, Account] = {
    2001: Account(id=2001, owner_user_id=1001, balance=1000.0),
    2002: Account(id=2002, owner_user_id=1002, balance=500.0),
    2003: Account(id=2003, owner_user_id=1002, balance=2500.0),
}


def decode_token(auth_header: Optional[str] = Header(None, alias="Authorization")) -> dict:
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


@app.get("/accounts/{account_id}/balance")
async def get_balance(account_id: int, token: dict = Depends(decode_token)):
    """Deliberately vulnerable: does NOT verify that the account belongs to the user.

    This is the core of the IDOR / broken access control scenario.
    """
    acct = ACCOUNTS.get(account_id)
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found")
    # Missing ownership check on purpose.
    return {"account_id": acct.id, "owner_user_id": acct.owner_user_id, "balance": acct.balance}


@app.post("/accounts/transfer")
async def transfer(body: TransferRequest, token: dict = Depends(decode_token)):
    """Simplified transfer endpoint.

    It partially trusts the token and only performs minimal checks, illustrating how
    weak authorization decisions can be abused.
    """
    from_acct = ACCOUNTS.get(body.from_account_id)
    to_acct = ACCOUNTS.get(body.to_account_id)
    if not from_acct or not to_acct:
        raise HTTPException(status_code=404, detail="Account not found")

    # Weak check: only ensures that the caller owns the *source* account.
    caller_user_id = int(token.get("sub"))
    if from_acct.owner_user_id != caller_user_id:
        raise HTTPException(status_code=403, detail="Not allowed to transfer from this account")

    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if from_acct.balance < body.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    from_acct.balance -= body.amount
    to_acct.balance += body.amount

    return {
        "status": "ok",
        "from_account_id": from_acct.id,
        "to_account_id": to_acct.id,
        "amount": body.amount,
        "caller_user_id": caller_user_id,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
