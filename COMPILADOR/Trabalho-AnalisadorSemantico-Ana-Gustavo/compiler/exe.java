package compiler;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import lexical.*;
import syntatic.*;

public class exe {

    public static void main(String[] args) {
        File pastaTestes = new File("testes");
        File[] arquivos = pastaTestes.listFiles((dir, name) -> name.endsWith(".txt"));

        if (arquivos == null || arquivos.length == 0) {
            System.out.println("Nenhum arquivo de teste encontrado na pasta 'testes'.");
            return;
        }

        for (File arquivo : arquivos) {
            System.out.println("Analisando: " + arquivo.getName());

            try (LexicalAnalysis lex = new LexicalAnalysis(new FileInputStream(arquivo))) {
                SyntaticAnalysis syn = new SyntaticAnalysis(lex); 
                syn.process();
                System.out.println("Análise Semântica realizada com sucesso");   
            } catch (IOException e) {
                System.err.println("Erro ao ler o arquivo: " + arquivo.getName());
            } catch (Exception e) {
                System.err.println("Erro ao analisar código " + e.getMessage());
            }

            System.out.println(""); 
        }
    }
}
