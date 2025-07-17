package com.jenkins.practice.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class DemoController {

    private static final Logger logger = LoggerFactory.getLogger(DemoController.class);

    @Value("${client.db.name:default_db}")
    private String clientDbName;

    @Value("${client.email.support:support@example.com}")
    private String supportEmail;

    @Value("${feature.flag:false}")
    private boolean featureFlag;

    @GetMapping("/demoOfJenkins")
    public String helloFromJenkins() {
        logger.info("Accessed /demoOfJenkins | DB: {}, Email: {}, FeatureFlag: {}", clientDbName, supportEmail, featureFlag);
        return "Connected to DB: " + clientDbName + " | Email: " + supportEmail + " | Feature: " + (featureFlag ? "ENABLED" : "DISABLED");
    }
}