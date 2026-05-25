#include <iostream>
#include <string>

int main() {
    std::cout << "[M82 C++ Core] Iniciando análisis estructural de alta velocidad..." << std::endl;
    
    double brent_crude = 98.83;
    double sp500_futuros = 0.7;
    std::string estatus_ormuz = "BLOQUEADO_PERO_NEGOCIANDO";

    std::cout << "[M82 C++ Core] Brent Crude: $" << brent_crude << " | Futuros S&P 500: +" << sp500_futuros << "%" << std::endl;
    std::cout << "[M82 C++ Core] Estatus Canal: " << estatus_ormuz << std::endl;

    if (brent_crude > 95.0 && estatus_ormuz == "BLOQUEADO_PERO_NEGOCIANDO") {
        std::cout << "⚠️ CRÍTICO: Riesgo latente en el Estrecho de Ormuz activo." << std::endl;
    } else {
        std::cout << "✅ BALANCEADO: Fluidez macro estable." << std::endl;
    }

    return 0;
}
