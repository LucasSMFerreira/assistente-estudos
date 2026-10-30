from pathlib import Path

from pypdf import PdfReader


def ler_pdf(caminho: Path) -> list[str]:
    """Retorna o texto de cada página de um arquivo PDF."""
    leitor = PdfReader(caminho)
    return [pagina.extract_text() or "" for pagina in leitor.pages]
