package com.mycompany.geneticomochila;

import java.util.*;

public class Algoritmo {
    private List<Item> itens;
    private int peso_Max;
    private int tamanho_Populacao;
    private double taxa_Mutacao;
    private double taxa_Crossover;
    private int num_Geracoes;

    private Mochila mochila;

    public Algoritmo(List<Item> itens, int peso_Max, int tamanho_Populacao, double taxa_Mutacao, double taxa_Crossover, int num_Geracoes) {
        this.itens = itens;
        this.peso_Max = peso_Max;
        this.tamanho_Populacao = tamanho_Populacao;
        this.taxa_Mutacao = taxa_Mutacao;
        this.taxa_Crossover = taxa_Crossover;
        this.num_Geracoes = num_Geracoes;
        this.mochila = new Mochila(peso_Max);
    }

    public void executar() {
        
        long tempoInicial = System.currentTimeMillis();

        //Populacao inicial:
        List<boolean[]> populacao = new ArrayList<>();
        
        Random rand = new Random();
        
        for (int i = 0; i < tamanho_Populacao; i++) {
            //Cria um vetor de boolean do tamanho do vetor de itens
            //pq cada boolean representa a existencia ou n do item
            boolean[] individuo = new boolean[itens.size()];
            for (int j = 0; j < individuo.length; j++) {
                if(rand.nextBoolean())
                    individuo[j] = true;
                else                
                    individuo[j] = false;
            }
            populacao.add(individuo);
        }
        
        //Vai de geração em geração:
        System.out.println("Geração | Melhor:| Pior:| Média:");
        for (int geracao = 0; geracao < num_Geracoes; geracao++) {
            // CRIA O VETOR FITNESS QUE CARREGA O VALOR DA MOCHILA PARA CADA INDIVIDUO
            List<Integer> fitnesses = new ArrayList<>();
            //PREENCHE O VETOR FITNESS
            for (boolean[] individuo : populacao) {
                fitnesses.add(mochila.calcularFitness(individuo, itens));
            }
            
            //Para salvar os dados:
            int melhor = Collections.max(fitnesses);
            int pior = Collections.min(fitnesses);
            double media = fitnesses.stream().mapToInt(Integer::intValue).average().orElse(0);
            
            // Imprime 
            System.out.printf("%d  %d  %d  %.4f%n", geracao, melhor, pior, media);
            
            // FUNCIONAMENTO DO ALGORITMO:
            //Criar nova população:
            List<boolean[]> nova_Populacao = new ArrayList<>();
            //Essa nova população se dá atraves da seleção dos paia, por sorteio,
            //Depois se dá a combinação genética e por fim a mutação:
            for(int i = 0; i<tamanho_Populacao;i++){
                boolean[] pai_1 = selecaoTorneio(populacao, fitnesses);
                boolean[] pai_2 = selecaoTorneio(populacao, fitnesses);
                boolean[] filho = crossover(pai_1, pai_2);
                mutar(filho);
                nova_Populacao.add(filho);
            }

            populacao = nova_Populacao;
            
        }
        
        System.out.println("o metodo executou em " + (System.currentTimeMillis() - tempoInicial));

    }

    private boolean[] selecaoTorneio(List<boolean[]> populacao, List<Integer> fitnesses) {
        Random rand = new Random();
        int i1 = rand.nextInt(tamanho_Populacao);
        int i2 = rand.nextInt(tamanho_Populacao);
        //retorna o com melhor fitness:
        if(fitnesses.get(i1) > fitnesses.get(i2)) return populacao.get(i1);
        
        return populacao.get(i2);
    }

        //
    private boolean[] crossover(boolean[] pai1, boolean[] pai2) {
        Random rand = new Random();
        //cria o filho
        boolean[] filho = new boolean[pai1.length];
        //Vê se faz o crossover ou não:
        if (rand.nextDouble() < taxa_Crossover) {
            //preenche a informação genetica:
            // Cria um ponto aleatorio: 
            int ponto = rand.nextInt(pai1.length);
            //A partir desse ponto altera o dna entre pai um e pai 2
            for (int i = 0; i < pai1.length; i++) {
                if((i < ponto))
                    filho[i] = pai1[i];
                else
                    filho[i] = pai2[i];
            }
        } else {
            //Só copia os dados do pai
            filho = Arrays.copyOf(pai1, pai1.length);
        }
        return filho;
    }

    private void mutar(boolean[] individuo) {
        //muda um bit aleatório:
        Random rand = new Random();
        if (rand.nextDouble() < taxa_Mutacao) {
            //inverte o valor do bit
            int i = rand.nextInt(itens.size());
            individuo[i] = !individuo[i];
        }  
    }
    
}
