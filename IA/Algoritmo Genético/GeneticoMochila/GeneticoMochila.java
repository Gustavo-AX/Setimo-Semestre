package com.mycompany.geneticomochila;

import java.util.*;

public class GeneticoMochila {   
    public static void main(String[] args) {
        //gera os itens aleatórios:
        List<Item> itens = new ArrayList<>();
        Random rand = new Random();
        for (int i = 0; i < 25; i++) {
            itens.add(new Item(rand.nextInt(1, 26), rand.nextInt(10, 101)));
        }
        
        //chama a função com os parametros definidos:
        Algoritmo ag = new Algoritmo(itens, 500, 100, 0.5, 0.3, 100);

        ag.executar();
    }  
}
