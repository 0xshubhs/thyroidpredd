# Thyroid Prediction Using Machine Learning

A web application that predicts a thyroid-disease class from a set of clinical
measurements (age, TSH, T3, TT4, T4U, FTI, etc.) using a trained machine-learning
model. It is a two-part project: a **React** frontend and a **Flask** backend that
serves a pickled scikit-learn model.

> Status: work-in-progress / partially finished. The prediction path works
> end-to-end, but several pages and features are stubs. See
> [Status / What's incomplete](#status--whats-incomplete).

## Stack

| Layer     | Technology                                                        |
|-----------|-------------------------------------------------------------------|
| Frontend  | React 18 (Create React App), React Router, SCSS modules, Tailwind |
| Backend   | Flask, scikit-learn (`LogisticRegression`), NumPy                 |
| Model     | Pickled model at `backend/model.sav` (10 input features)          |
| Notebooks | EDA + model training under `backend/thyroid/`                     |

## Repository layout

```
backend/
  server.py                     # Flask API (POST /thyroidpredict)
  model.sav                     # Pickled scikit-learn model used at runtime
  requirements.txt              # Python dependencies
  thyroid/
    Thyroid Disease Detection_EDA.ipynb
    Model Training.ipynb        # Trains a RandomForest, saves Thyroid_model.pkl
    Thyroid_Data.csv            # Raw dataset
    Preprocessed_data.csv       # Cleaned/encoded dataset used for training
frontend/
  src/
    App.js                      # Routes: /, /Home, /prediction, /Blogs, /Login, /Awareness
    components/                 # Home, Prediction, NavBar, Footer, Awareness, Blogs, Login
  build/                        # Pre-built production bundle (committed)
```

## Prerequisites

- Python 3.9+ (verified on 3.14)
- Node.js 18+ and npm (for the frontend)

## Setup & run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py                 # serves on http://localhost:5000
```

Test the endpoint directly:

```bash
curl -X POST http://localhost:5000/thyroidpredict \
  -H "Content-Type: application/json" \
  -d '{"age":45,"TSH":2.5,"pregnant":0,"T3":1.8,"TT4":110,"on_thyroxine":0,"T4U":1.1,"FTI_measured":1,"tumor":0,"FTI":95}'
# -> "Primary hypothyroid"
```

The API accepts JSON with the fields above and returns one of:
`Compensated hypothyroid`, `No thyroid`, `Primary hypothyroid`, `Secondary hypothyroid`.

### Frontend

```bash
cd frontend
npm install
npm start                        # dev server on http://localhost:3000
```

`package.json` sets `"proxy": "http://localhost:5000/"`, so the frontend's
relative `POST /thyroidpredict` call is forwarded to the Flask backend during
development. Run the backend on port 5000 for the prediction form to work.

## API

`POST /thyroidpredict` — request body (JSON):

| Field          | Type  | Notes                          |
|----------------|-------|--------------------------------|
| `age`          | int   |                                |
| `TSH`          | float | Thyroid Stimulating Hormone    |
| `pregnant`     | 0/1   |                                |
| `T3`           | float | Triiodothyronine               |
| `TT4`          | float | Total Thyroxine                |
| `on_thyroxine` | 0/1   |                                |
| `T4U`          | float |                                |
| `FTI_measured` | 0/1   |                                |
| `tumor`        | 0/1   |                                |
| `FTI`          | float | Free Thyroxine Index           |

Response: a plain-text label string (see values above).

## Status / What's incomplete

Inferred from the current code — not a roadmap of promised features.

- **Model vs. training notebook mismatch.** `Model Training.ipynb` trains a
  `RandomForestClassifier` and saves it as `Thyroid_model.pkl` using an
  11-feature set (`age, sex, TSH, TT4, FTI, on_thyroxine,
  on_antithyroid_medication, goitre, hypopituitary, psych, T3_measured`).
  The backend instead loads `model.sav`, which is a **`LogisticRegression`
  trained on a different 10-feature set** (the fields the API accepts). The
  notebook does not produce `model.sav`; its provenance/preprocessing is not
  reproducible from this repo.
- **scikit-learn version drift.** `model.sav` was pickled with scikit-learn
  0.24.2; newer versions load it but emit an `InconsistentVersionWarning`.
  Results are not guaranteed identical across versions. Retraining is the fix.
- **No input scaling at inference.** The training notebook applies a
  `StandardScaler` and encoders, but `server.py` feeds raw values straight to
  the model with no scaler. If `model.sav` expects scaled inputs, predictions
  may be unreliable.
- **Frontend pages are partial:**
  - `Login.jsx` renders a placeholder `<div>Login</div>` — no auth.
  - `Blogs.jsx` contains hard-coded crisis-helpline content, not thyroid blogs.
  - `Home.jsx` / `Awareness.jsx` are static informational pages.
- **Unused dependencies.** `package.json` pulls in `firebase`, `web3`,
  `@metamask/sdk-react`, `agora-rtc-sdk-ng`, and `react-redux`, but none are
  referenced in `src/`. No Firebase/auth/web3 features are implemented.
- **Default CRA test only.** `App.test.js` is the boilerplate "renders learn
  react link" test and does not match the app; it will fail as-is.
- **No deployment config** (no Dockerfile, no production WSGI server; Flask runs
  in debug mode).

## License

See [LICENSE](LICENSE).
