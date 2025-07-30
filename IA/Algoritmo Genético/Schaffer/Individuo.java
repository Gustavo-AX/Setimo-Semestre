package com.mycompany.schaffer;

public class Individuo {
    public double fitness;
    //x e y
    public double[] codigo;
    
    public Individuo(){
        this.codigo = new double[2];
        this.codigo[0] = Math.random() * 10;
        this.codigo[1] = Math.random() * 10;
        fitness();
    }
    
    public void fitness(){
        fitness = 0.5 - ((Math.pow(Math.sin(Math.sqrt(codigo[0] * codigo[0] + codigo[1] * codigo[1])), 2) - 0.5) / Math.pow(1.0 + 0.001 * (codigo[0] * codigo[0] + codigo[1] * codigo[1]), 2));
    }
    
}
