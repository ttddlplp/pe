package specs.acceptanceTest;

import org.concordion.integration.junit4.ConcordionRunner;
import org.junit.Before;
import org.junit.runner.RunWith;

import com.gzeng.pe.backend.webservice.HelloWorld;

/* Run this class as a JUnit test. */

@RunWith(ConcordionRunner.class)
public class ForFunFixture {
    
    private HelloWorld helloWorld;

    @Before
    public void setUp() {
        helloWorld = new HelloWorld();
    }
    
    public String getGreeting() {
        return helloWorld.getMessage();
    }
}
