import requests
import time
import psycopg2

class MonitoringAgent:
    def __init__(self, config: dict):
        self.config = config

    def run_task(self, task: dict):
        action = task.get("action")
        if action == "health_check":
            return self.health_check()
        else:
            return {"status": "ERROR", "message": f"Ação desconhecida: {action}"}

    def _check_service(self, service_name: str, url: str):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency_ms = round((time.time() - start_time) * 1000)
            if response.status_code == 200:
                return {"service": service_name, "status": "OK", "details": f"API respondeu com status {response.status_code} OK.", "latency_ms": latency_ms}
            else:
                return {"service": service_name, "status": "ERROR", "details": f"API respondeu com status {response.status_code}.", "latency_ms": latency_ms}
        except requests.RequestException as e:
            latency_ms = round((time.time() - start_time) * 1000)
            return {"service": service_name, "status": "ERROR", "details": str(e), "latency_ms": latency_ms}

    def _check_postgresql(self):
        db_config = self.config.get("postgresql", {})
        start_time = time.time()
        try:
            conn = psycopg2.connect(
                dbname=db_config.get("dbname"),
                user=db_config.get("user"),
                password=db_config.get("password"),
                host=db_config.get("host"),
                port=db_config.get("port", 5432)
            )
            conn.close()
            latency_ms = round((time.time() - start_time) * 1000)
            return {"service": "PostgreSQL", "status": "OK", "details": "Conexão estabelecida com sucesso.", "latency_ms": latency_ms}
        except psycopg2.Error as e:
            latency_ms = round((time.time() - start_time) * 1000)
            return {"service": "PostgreSQL", "status": "ERROR", "details": str(e).strip(), "latency_ms": latency_ms}

    def _check_ollama(self):
        return self._check_service("Ollama API", self.config.get("ollama_api_url", "http://localhost:11434"))

    def _check_litellm(self):
        return self._check_service("LiteLLM Gateway", self.config.get("litellm_gateway_url", "http://localhost:4000"))

    def _check_mcp_servers(self):
        mcp_urls = self.config.get("mcp_server_urls", [])
        if not mcp_urls:
            return {"service": "MCP Servers", "status": "NOT_CONFIGURED", "details": "Nenhum servidor MCP configurado."}
        
        results = [self._check_service(f"MCP Server #{i+1}", url) for i, url in enumerate(mcp_urls)]
        
        if all(res["status"] == "OK" for res in results):
            return {"service": "MCP Servers", "status": "OK", "details": f"Todos os {len(mcp_urls)} servidores MCP configurados estão respondendo."}
        else:
            return {"service": "MCP Servers", "status": "ERROR", "details": "Um ou mais servidores MCP não estão respondendo.", "sub_results": results}

    def health_check(self):
        results = [
            self._check_postgresql(),
            self._check_ollama(),
            self._check_litellm(),
            self._check_mcp_servers(),
        ]

        overall_status = "OK"
        if any(res["status"] == "ERROR" for res in results):
            overall_status = "ERROR"
        elif any(res["status"] == "NOT_CONFIGURED" for res in results):
            overall_status = "NEEDS_ATTENTION"

        return {
            "overall_status": overall_status,
            "health_results": results
        }
