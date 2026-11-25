# CompetitorAI: desktop app

A PyQt6 app with the same modes as the web interface: text analysis, image analysis (you can drag a file into the window), website analysis by link and the history of the last 10 requests. The look follows the web version: a dark theme, a side navigation panel, cards with forms.

The analysis itself is done by the project's server, so the server must be running on `http://localhost:8000` before you start the app.

## Running it

```bash
# in the project root
python run.py

# in another terminal
cd desktop
pip install -r requirements.txt
python main.py
```

## Building

Windows; `CompetitorMonitor.exe` appears in `dist/`:

```bash
cd desktop
python build.py
```

macOS, a `.app` bundle:

```bash
cd desktop
python build_mac.py
```

Remove build artifacts: `python build.py clean`.

The built app also talks to the server, which has to be started separately. Bundling the server into the app isn't done yet.

## Files

- `main.py`: the main window.
- `styles.py`: the dark theme.
- `api_client.py`: HTTP client for the server.
- `build.py`, `build_mac.py`, `CompetitorMonitor.spec`: building with PyInstaller.
