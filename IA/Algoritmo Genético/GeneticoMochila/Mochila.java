package com.mycompany.geneticomochila;

import java.util.List;

public class Mochila {
    private int pesoMax;

    public Mochila(int pesoMax) {
        this.pesoMax = pesoMax;
    }
    
    
    //O Fitness é o valor
    public int calcularFitness(boolean[] individuo, List<Item> itens) {
        int pesoTotal = 0;
        int valorTotal = 0;
        int quantidade = 0;

        for (int i = 0; i < individuo.length; i++) {
            if (individuo[i]) {
                pesoTotal += itens.get(i).getPeso();
                valorTotal += itens.get(i).getValor();
                quantidade++;
            }
        }

        if (pesoTotal > pesoMax || quantidade > 30) return 0;
        return valorTotal;
    }
}
