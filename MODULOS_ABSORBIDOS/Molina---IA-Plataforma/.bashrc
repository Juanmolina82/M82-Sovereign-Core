alias M='pkill -f cloudflared; pkill -f streamlit; python3 -m streamlit run m82_quantum_v2.py --server.port 8501 --server.address 127.0.0.1 & sleep 10; cloudflared tunnel --url http://127.0.0.1:8501'
