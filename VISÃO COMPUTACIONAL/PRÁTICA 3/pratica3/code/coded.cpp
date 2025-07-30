#include "CImg.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace cimg_library;
using namespace std;

int main() {
    const char* imagem = "../imagens/perfil_pessoa.bmp";
    CImg<float> img(imagem);
    img = img.channel(0);  // escala de cinza

    // Erosão
    CImg<float> erodida = img.get_erode(3);

    // A - (A 0 B)
    CImg<float> borda = img - erodida;

    // Salva resultado
    borda.save("imagem_fronteira.bmp");

    // Perímetro
    int perimetro = 0;
    cimg_forXY(borda, x, y) {
        if (borda(x, y) > 0) ++perimetro;
    }

    // Área
    int area = 0;
    cimg_forXY(img, x, y) {
        if (img(x, y) > 0) ++area;
    }

    cout << "Perímetro estimado (pixels na borda): " << perimetro << endl;
    cout << "Área estimada (pixels > 0 na imagem): " << area << endl;

    return 0;
}


