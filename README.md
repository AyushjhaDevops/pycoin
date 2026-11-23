# PyCoin (PYC)

**An educational cryptocurrency and blockchain implementation built with Python and React.**

PyCoin is a learning-focused project designed to explore the engineering principles behind cryptocurrencies, blockchain data structures, cryptographic security, digital signatures, transactions, mining, and Proof of Work consensus.

> **Project status:** Phase 0 — Project Initialization

## Project objectives

- Understand cryptocurrency architecture by implementing core components.
- Build cryptographic primitives and digital signatures.
- Implement a blockchain and transaction engine.
- Develop a Proof of Work mining and consensus mechanism.
- Create a wallet and blockchain explorer interface.
- Build a React frontend connected to a Python API.

## Technology stack

| Component | Technology |
|---|---|
| Core language | Python |
| Backend API | FastAPI |
| Data validation | Pydantic |
| Database | SQLite |
| ORM and migrations | SQLAlchemy, Alembic |
| Cryptography | PyNaCl, hashlib |
| Frontend | React, Vite |
| Frontend testing | Vitest, Testing Library |
| Backend testing | Pytest, HTTPX |
| Code quality | Ruff |
| Version control | Git, GitHub |

## Project structure

```text
pycoin/
├── backend/
│   ├── pycoin/
│   │   ├── api/
│   │   ├── consensus/
│   │   ├── core/
│   │   ├── crypto/
│   │   ├── network/
│   │   ├── storage/
│   │   ├── transactions/
│   │   ├── wallet/
│   │   ├── config.py
│   │   ├── main.py
│   │   └── __main__.py
│   └── tests/
├── frontend/
├── documentation/
├── infrastructure/
├── scripts/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Getting started

### Prerequisites

- Python 3.12 or later
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/AyushjhaDevops/pycoin.git
cd pycoin
```

### 2. Set up the Python backend

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Review `.env` and adjust settings if required. Never commit secrets or private keys.

### 4. Run the backend

```bash
python -m pycoin
```

Backend: `http://127.0.0.1:8000`

API documentation: `http://127.0.0.1:8000/docs`

Health endpoint: `http://127.0.0.1:8000/api/v1/health`

### 5. Set up the React frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://127.0.0.1:5173`

## Testing

### Backend

From the project root, with the virtual environment activated:

```bash
python -m pytest -v
python -m ruff check backend
python -m ruff format --check backend
```

### Frontend

```bash
cd frontend
npm test
npm run build
```

## Development roadmap

| Phase | Description |
|---|---|
| 0 | Project initialization and development environment |
| 1 | Cryptographic foundation |
| 2 | Blockchain data structures |
| 3 | Transaction engine |
| 4 | Wallet implementation |
| 5 | Mempool |
| 6 | Proof of Work mining |
| 7 | Consensus mechanism |
| 8 | Persistent blockchain storage |
| 9 | Peer-to-peer networking |
| 10 | Blockchain synchronization |
| 11 | REST API |
| 12 | React wallet |
| 13 | Blockchain explorer |
| 14 | Security and comprehensive testing |
| 15 | Deployment and final documentation |

## Security and educational disclaimer

PyCoin is an educational project. It is intended for local development and experimentation, not for handling real funds or production cryptocurrency operations.

Do not use real private keys or valuable assets with this project. A production cryptocurrency requires independent security reviews, extensive testing, and careful protocol design.

## License

This project is licensed under the MIT License. See the `LICENSE` file when added to the repository.