#include "CImg.h"
#include <iostream>
// Use the library namespace to ease the declarations afterward.
using namespace cimg_library;
using namespace std;
int main()
{
  // Carrega imagem
  char str[] = "./imagens/lena_cinza.bmp";
  char str2[] = "./imagens/olho.bmp";
  CImg<unsigned char> image1(str); // image is initialized by reading an image file from the disk
  CImg<unsigned char> image2(str2);
  // Calcula distancia entre linhas para desenhar
  int largura, altura, num_linhas;
  int x, y;
  largura = image1.width();
  altura = image1.height();

  for (y = 0; y < altura; y++)
  { // para cada linha
    for (x = 0; x < largura; x++)
    {                                       
      if(image1(x, y, 0, 0) * image2(x, y, 0, 0) > 255 || image1(x, y, 0, 1) * image2(x, y, 0, 1) > 255 || image1(x, y, 0, 1) * image2(x, y, 0, 1) > 255){
      image1(x, y, 0, 0) = 255; // Red component of image sent to imgR
      image1(x, y, 0, 1) = 255;
      image1(x, y, 0, 2) = 255;
      } else if(image1(x, y, 0, 0) * image2(x, y, 0, 0) < 0 || image1(x, y, 0, 1) * image2(x, y, 0, 1) < 0 || image1(x, y, 0, 2) * image2(x, y, 0, 2) < 0){
      image1(x, y, 0, 0) = 0;
      image1(x, y, 0, 1) = 0;
      image1(x, y, 0, 2) = 0;
      } else{
        image1(x, y, 0, 0) = image1(x, y, 0, 0) * image2(x, y, 0, 0); // Red component of image sent to imgR
        image1(x, y, 0, 1) = image1(x, y, 0, 1) * image2(x, y, 0, 1);
        image1(x, y, 0, 2) = image1(x, y, 0, 2) * image2(x, y, 0, 2);
      }
    }
  }

  // Salva a imagem em arquivo bmp
  image1.save("imagem_soma.bmp");
  return 0;
}
