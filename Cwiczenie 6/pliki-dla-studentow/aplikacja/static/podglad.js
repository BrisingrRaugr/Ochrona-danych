// Podglad tekstu przekazanego po znaku # w adresie.
// textContent wstawia wartosc jako zwykly tekst, wiec HTML nie jest interpretowany (brak XSS DOM).
document.getElementById("podglad").textContent = decodeURIComponent(location.hash.slice(1));
