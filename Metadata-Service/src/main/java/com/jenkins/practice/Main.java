package com.jenkins.practice;

import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        FileWriter writer = new FileWriter("metadata-output.txt", true);
        writer.write("Metadata Service: Metadata written via Jenkins build!\n");
        writer.close();
        System.out.println("✅ File written!");
    }
}