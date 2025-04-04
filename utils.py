def format_number(value, prefix=""):
    for unit in ["", " mil"]:
        if value < 1000:
            return f"{prefix}{value:.2f}{unit}"
        value /= 1000  # Corrigido aqui
    return f"{prefix}{value:.2f} milhões"

def formatar_input(valor):
    return float(str(valor).replace(',', '.'))


