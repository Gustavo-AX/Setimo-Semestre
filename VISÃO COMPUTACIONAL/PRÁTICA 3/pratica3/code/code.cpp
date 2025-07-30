#include "CImg.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace cimg_library;
using namespace std;

int main()
{
    const char* str = "../imagens/perfil_pessoa.bmp";
    CImg<float> img(str);
    img = img.channel(0); // converte para cinza

    // 2 = Sobel
    CImgList<float> gradiente = img.get_gradient("xy", 2);
    CImg<float> gradiente_x = gradiente[0], gradiente_y = gradiente[1];

    // A imagem de resultado deverá ser obtida a partir da resposta do valor absoluto dos dois 
    // componentes do gradiente, |gx| e |gy|. A imagem do gradiente será formada pela soma desses dois 
    // componentes. 
    // |gradiente_c| + |gradiente_y|
    CImg<float> gradiente_soma = gradiente_x.get_abs() + gradiente_y.get_abs();
    
    /*// Para média da lena_cinza
    CImg<float> gradiente_media = (gradiente_x.get_abs() + gradiente_y.get_abs()) / 2;
    gradiente_media.normalize(0, 255);
    gradiente_media.save("lena_gradiente_media.bmp");*/
       
    //gradiente_soma.normalize(0, 255);
    gradiente_soma.save("bordas_sobel.bmp");

    return 0;
}


