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

    CImg<unsigned char> dilatada = img;

    int iteracoes = 10;
    
    dilatada = dilatada.get_dilate(3); // dilatação com elemento 3x3
    
    //Para ver quantas iterações, CUIDADO, VAI GERAR VARIAS IMAGENS KKK
    /*for (int i = 1; i <= iteracoes; ++i) {
        dilatada = dilatada.get_dilate(3); // dilatação com elemento 3x3

        string nome_saida = "opencv_dilatada_" + to_string(i) + ".bmp";
        dilatada.save(nome_saida.c_str());
    }*/
    
    dilatada.save("imagem_dilatada.bmp");

    return 0;
}


