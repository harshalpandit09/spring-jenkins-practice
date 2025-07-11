package com.jenkins.practice;

import java.io.FileWriter;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        FileWriter writer = new FileWriter("sql-output.txt", true);
        writer.write("SQL Service: Text written via Jenkins build!\n");
        writer.close();
        System.out.println("✅ File written!");
    }
}