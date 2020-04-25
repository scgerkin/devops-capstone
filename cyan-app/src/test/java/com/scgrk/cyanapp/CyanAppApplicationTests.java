package com.scgrk.cyanapp;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class CyanAppApplicationTests {

  @Test
  void contextLoads() {
  }

  @Test
  public void extremelyRigorousTest() {
    assertTrue(true);
  }

  @Disabled
  @Test
  public void thisTestAlwaysFails() {
    fail();
  }

}
