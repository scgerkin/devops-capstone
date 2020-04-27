package com.scgrk.cyanapp;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

@RestController
public class CyanController {

  @GetMapping("/")
  public ModelAndView getIndex() {
    return new ModelAndView("index");
  }
}
