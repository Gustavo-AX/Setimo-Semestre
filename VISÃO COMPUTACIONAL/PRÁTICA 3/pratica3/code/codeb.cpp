#include "CImg.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace cimg_library;
using namespace std;

int main()
{
    const char* imagem = "../imagens/circulos.bmp";
    CImg<float> img(imagem);
    img = img.channel(0);  // escala de cinza

    // Erosão 3x3
    CImg<float> erosao = img.get_erode(10);

    erosao.save("circulos.bmp");

    return 0;
}


