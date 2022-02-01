# # Create venv
# python -m venv .venv

# Install into virtual env and start server
.venv/bin/python -m pip install -r requirements.txt && \
.venv/bin/activate && func host start