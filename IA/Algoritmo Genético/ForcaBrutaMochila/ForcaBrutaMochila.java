package com.mycompany.forcabrutamochila;

import java.util.Random;

public class ForcaBrutaMochila {

    public static void main(String[] args) {
        long tempoInicial = System.currentTimeMillis();
        int numeroItensUniverso = 10;
        int pesoMaxMochila = 50;
        Item[] itens = new Item[numeroItensUniverso];
        Random random = new Random();

        for (int i = 0; i < numeroItensUniverso; i++) {
            itens[i] = new Item(random.nextInt(1, 26), random.nextInt(10, 101));
        }

        int melhorValor = 0;
        String melhorCombinacao = "";
        
        for (int i = 0; i < Math.pow(2, numeroItensUniverso); i++) {
            String binario = String.format("%" + numeroItensUniverso + "s", Integer.toBinaryString(i)).replace(' ', '0');
            int pesoTotal = 0;
            int valorTotal = 0;
            int quantidade = 0;

            for (int j = 0; j < numeroItensUniverso; j++) {
                if (binario.charAt(j) == '1') {
                    pesoTotal += itens[j].peso;
                    valorTotal += itens[j].valor;
                    quantidade++;
                }
            }

            if (pesoTotal <= pesoMaxMochila && valorTotal > melhorValor && quantidade <= 30) {
                melhorValor = valorTotal;
                melhorCombinacao = binario;
            }
            
            //System.out.println(binario);
        }

        System.out.println("Melhor combinação: " + melhorCombinacao);
        System.out.println("Valor total: " + melhorValor);
        
        System.out.println("o metodo executou em " + (System.currentTimeMillis() - tempoInicial));
    }
}