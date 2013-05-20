package com.gzeng.pe.backend.webservice;

import com.sun.jersey.api.core.ResourceConfig;
import com.sun.jersey.spi.container.WebApplication;
import com.sun.jersey.spi.container.servlet.ServletContainer;

public class WSServletContainer extends ServletContainer{
    
    /**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	@Override
    protected final void initiate(ResourceConfig rc, WebApplication wa) {
        super.initiate(rc, wa);
    }
}
