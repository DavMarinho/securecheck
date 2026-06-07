import streamlit as st
from scanner import scan_website
from report import generate_pdf


st.set_page_config(page_title="SecureCheck", page_icon="🔐", layout="centered")

st.title("🔐 SecureCheck")
st.caption("Auditoria de segurança web — headers HTTP e certificado SSL")

url = st.text_input("Digite a URL do site:", placeholder="exemplo.com")

if st.button("Analisar", type="primary"):
    if not url.strip():
        st.warning("Por favor, informe uma URL.")
    else:
        with st.spinner("Auditando o site..."):
            report = scan_website(url.strip())

        # Score visual
        score = report["score"]
        if score >= 80:
            st.success(f"Score: {score}/100 — {report['passed']}/{report['total']} verificações aprovadas")
        elif score >= 50:
            st.warning(f"Score: {score}/100 — {report['passed']}/{report['total']} verificações aprovadas")
        else:
            st.error(f"Score: {score}/100 — {report['passed']}/{report['total']} verificações aprovadas")

        st.divider()

        # Lista de verificações
        for c in report["checks"]:
            icon = {"ok": "✅", "warn": "⚠️", "fail": "❌"}.get(c["status"], "•")
            with st.expander(f"{icon} {c['name']}"):
                st.write(c["detail"])

        st.divider()

        # Botão de download do PDF
        pdf_bytes = generate_pdf(report)
        st.download_button(
            label="📄 Baixar relatório PDF",
            data=pdf_bytes,
            file_name=f"securecheck_{report['scanned_at'].replace('/', '-').replace(' ', '_').replace(':', '-')}.pdf",
            mime="application/pdf",
        )

st.divider()
st.caption("Desenvolvido por Davi Marinho · github.com/DavMarinho")