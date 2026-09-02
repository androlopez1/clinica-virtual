while true; do
  echo -n "Tú: "
  read msg
  echo "Asistente:"
  curl -s -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$msg\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
  echo ""
done
