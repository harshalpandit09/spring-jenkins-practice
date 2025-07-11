package com.jenkins.practice.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DemoController {
    @GetMapping("/demoOfJenkins")
    public String helloFromJenkins() {
        return "✅ Hello from Jenkins Demo Spring Boot API!";
    }
}