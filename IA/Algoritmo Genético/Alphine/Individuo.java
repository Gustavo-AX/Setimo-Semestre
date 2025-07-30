package com.mycompany.alphine;

public class Individuo {
    public double fitness;
    public double[] codigo;
    
    public Individuo(){
        this.codigo = new double[2];
        this.codigo[0] = Math.random() * 10;
        this.codigo[1] = Math.random() * 10;
        fitness();
    }
    
    public void fitness(){
        fitness = Math.sqrt(codigo[0]) * Math.sin(codigo[0]) * Math.sqrt(codigo[1]) * Math.sin(codigo[1]);
    }
}
