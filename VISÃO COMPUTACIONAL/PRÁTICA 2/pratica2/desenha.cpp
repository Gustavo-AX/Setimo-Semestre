#include "CImg.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

// Use the library namespace to ease the declarations afterward.
using namespace cimg_library;
using namespace std;
int main()
{
    // Carrega imgm
    char str[] = "moire.bmp";
    CImg<unsigned char> img(str); 

    img = img.channel(0);

    CImgList<float> fft = img.get_FFT();

    CImg<float> parte_real(fft[0]);
    CImg<float> parte_imaginaria(fft[1]);

    // Centraliza os componentes da DFT (para aplicar o filtro corretamente)
    parte_real.shift(parte_real.width() / 2, parte_real.height() / 2, 0, 0, 2);
    parte_imaginaria.shift(parte_imaginaria.width() / 2, parte_imaginaria.height() / 2, 0, 0, 2);

    // Carrega filtro
    CImg<float> filtro("filtro_visualizacao.bmp");
    filtro = filtro.channel(0); // Garante que o filtro tem 1 canal
    filtro.resize(img.width(), img.height());

    // Aplica o filtro à DFT
    parte_real *= filtro;
    parte_imaginaria *= filtro;

    // Desfaz o shift (volta o centro para origem) antes da inversa
    parte_real.shift(parte_real.width() / 2, parte_real.height() / 2, 0, 0, 2);
    parte_imaginaria.shift(parte_imaginaria.width() / 2, parte_imaginaria.height() / 2, 0, 0, 2);

    // Reconstrói a imagem com a IFFT
    CImgList<float> dft_filtrada(parte_real, parte_imaginaria);
    CImg<float> img_filtrada = dft_filtrada.get_FFT(true)[0]; // Parte real da IFFT

    // Normaliza para salvar corretamente
    img_filtrada.normalize(0, 255);
    img_filtrada.save("img_filtrada.bmp");

    return 0;
}
