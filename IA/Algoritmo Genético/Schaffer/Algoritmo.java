package com.mycompany.schaffer;

import java.util.*;

public class Algoritmo {
    /*
    Tamanho da população:
    Forma de seleção:
    Tipo de crossover:
    Função de Fitness:
    Número de Gerações:
    Taxa de Crossover:
    Taxa de Mutação:*/

    //Faixas de valores: Entre 0 e 10
    private int tamanho_Populacao;
    //Forma de seleção: Torneio
    //Tipo de crossover: Corte
    //Função de fitness:
    private int num_Geracoes;
    private double taxa_Crossover;
    private double taxa_Mutacao;

    private Random rand = new Random();

    public Algoritmo(int tamanho_Populacao, double taxa_Mutacao, double taxa_Crossover, int num_Geracoes) {
        this.tamanho_Populacao = tamanho_Populacao;
        this.taxa_Mutacao = taxa_Mutacao;
        this.taxa_Crossover = taxa_Crossover;
        this.num_Geracoes = num_Geracoes;
    }

    public void executar() {
        List<Individuo> populacao = new ArrayList<>();

        // Inicializa a população:
        for (int i = 0; i < tamanho_Populacao; i++) {
            populacao.add(new Individuo());
        }
        //Cria um individuo para comparações futuras;
        Individuo melhor_Ultimo_Individuo = new Individuo();
        melhor_Ultimo_Individuo.fitness = 0;
        
        System.out.println("Geração | Melhor:| Pior:| Média:");

        for (int geracao = 1; geracao <= num_Geracoes; geracao++) {
            List<Individuo> nova_Populacao = new ArrayList<>();

            // Seleção:
            
            for (int i = 0; i < tamanho_Populacao; i++) {
                // Seleção por torneio:
                Individuo pai1 = torneio(populacao);
                Individuo pai2 = torneio(populacao);

                // Crossover dos pais:
                Individuo filho = crossover(pai1, pai2);

                // Mutação:
                mutar(filho);

                // Avaliação do filho
                filho.fitness();

                // Adiciona à nova população:
                nova_Populacao.add(filho);
            }

            // Substitui a população antiga
            populacao = nova_Populacao;

            // Estatísticas da geração
            double melhor = 0;
            int indice_melhor = 0;
            double pior = 100;
            int indice_pior = 0;
            double soma = 0;
            
            for(int i = 0; i< nova_Populacao.size(); i++){
                if (nova_Populacao.get(i).fitness > melhor){
                    melhor = nova_Populacao.get(i).fitness;
                    indice_melhor = i;
                }
                if (nova_Populacao.get(i).fitness < pior){
                    pior = nova_Populacao.get(i).fitness;
                    indice_pior = i;
                }   
            }
            
            if(melhor_Ultimo_Individuo.fitness > melhor){
                nova_Populacao.set(indice_pior, melhor_Ultimo_Individuo);
            }
            
            //Coisa de preguiçoso:
            melhor = 0;
            pior = 100;
            for(int i = 0; i< nova_Populacao.size(); i++){
                if (nova_Populacao.get(i).fitness > melhor){
                    melhor = nova_Populacao.get(i).fitness;
                }
                if (nova_Populacao.get(i).fitness < pior){
                    pior = nova_Populacao.get(i).fitness;
                }   
                soma += nova_Populacao.get(i).fitness;
            }
            

            double media = soma / tamanho_Populacao;

            // Imprime estatísticas da geração
            System.out.printf(" %d %.4f %.4f %.4f%n", geracao, melhor, pior, media);
        }
    }
    
    // Seleção por tornei, entre dois
    public Individuo torneio(List<Individuo> populacao) {
        Individuo a = populacao.get(rand.nextInt(tamanho_Populacao));
        Individuo b = populacao.get(rand.nextInt(tamanho_Populacao));
        if(a.fitness > b.fitness)
            return a;
        return b;
    }

    public Individuo crossover(Individuo pai1, Individuo pai2){
        Individuo filho = new Individuo();;
        if (rand.nextDouble() < taxa_Crossover) {
            filho.codigo[0] = (pai1.codigo[0] + pai2.codigo[0]) / 2;
            filho.codigo[1] = (pai1.codigo[1] + pai2.codigo[1]) / 2;

        } else {             
            filho.codigo[0] = pai1.codigo[0];
            filho.codigo[1] = pai1.codigo[1];
        }
        return filho;
    }

    private void mutar(Individuo individuo) {
        if (rand.nextDouble() < taxa_Mutacao) {
                individuo.codigo[0] = Math.random() * 10;
                individuo.codigo[1] = Math.random() * 10;
        }
    }

}
