import requests
import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse


SECURITY_HEADERS = {
    "Content-Security-Policy": "Previne ataques XSS controlando fontes de conteúdo permitidas.",
    "Strict-Transport-Security": "Força o navegador a usar HTTPS, prevenindo downgrade attacks.",
    "X-Frame-Options": "Previne clickjacking impedindo que o site seja embutido em iframes.",
    "X-Content-Type-Options": "Previne MIME sniffing, bloqueando interpretação errada de arquivos.",
    "Referrer-Policy": "Controla quais informações de referência são enviadas em requisições.",
}


def normalize_url(url: str) -> str:
    """Garante que a URL tenha schema."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def check_https(url: str) -> dict:
    """Verifica se o site usa HTTPS."""
    parsed = urlparse(url)
    is_https = parsed.scheme == "https"
    return {
        "name": "HTTPS Ativo",
        "status": "ok" if is_https else "fail",
        "detail": "Site usa HTTPS." if is_https
                  else "Site não usa HTTPS — tráfego não criptografado.",
    }


def check_ssl_certificate(url: str) -> dict:
    """Verifica validade do certificado SSL."""
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expire_str = cert["notAfter"]
                expire_date = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (expire_date - datetime.utcnow()).days

                if days_left < 0:
                    return {
                        "name": "Certificado SSL",
                        "status": "fail",
                        "detail": f"Certificado EXPIRADO há {abs(days_left)} dias.",
                    }
                if days_left < 30:
                    return {
                        "name": "Certificado SSL",
                        "status": "warn",
                        "detail": f"Certificado expira em {days_left} dias.",
                    }
                return {
                    "name": "Certificado SSL",
                    "status": "ok",
                    "detail": f"Certificado válido. Expira em {days_left} dias.",
                }
    except Exception as e:
        return {
            "name": "Certificado SSL",
            "status": "fail",
            "detail": f"Erro ao validar SSL: {str(e)}",
        }


def check_headers(url: str) -> list:
    """Verifica presença dos headers de segurança."""
    results = []
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers

        for header, description in SECURITY_HEADERS.items():
            if header in headers:
                results.append({
                    "name": header,
                    "status": "ok",
                    "detail": f"Presente. {description}",
                })
            else:
                results.append({
                    "name": header,
                    "status": "fail",
                    "detail": f"AUSENTE. Risco: {description}",
                })
    except requests.RequestException as e:
        results.append({
            "name": "Conexão",
            "status": "fail",
            "detail": f"Erro ao conectar: {str(e)}",
        })
    return results


def scan_website(url: str) -> dict:
    """Executa todas as verificações e retorna o relatório."""
    url = normalize_url(url)
    checks = [check_https(url), check_ssl_certificate(url)]
    checks.extend(check_headers(url))

    total = len(checks)
    passed = sum(1 for c in checks if c["status"] == "ok")
    score = round((passed / total) * 100)

    return {
        "url": url,
        "scanned_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "score": score,
        "passed": passed,
        "total": total,
        "checks": checks,
    }