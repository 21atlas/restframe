1.在本地使用curl http://localhost:80/v1/test返回对应的结果：{"name": "test", "properties": "test"}
2.代码逻辑流程如下：
   wsgisimpleserver
       ->urlmap
          ->myrouterapp(apirouter)
              ->__call__ reutrn routersmiddleware    routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.map)
              ->RoutesMiddleware __call__ 
                   config.environ = environ
                        load_wsgi_environ
                        result = mapper.routematch(path)
                    response = self.app(environ, start_response)  这个调用跑到一个_dispatch函数去了，也就是上面的self._dispatch，
                                                                  也就是wsgi.py文件内部的Router类的成员    @staticmethod @webob.dec.wsgify 
                                                                  def _dispatch(req): 该函数被系统的webob.dec.wsgify装饰了，所以先调用   
                                                                  dec.py文件内的wsgify的def __call__(self, req, *args, **kw):
                        ->dec.wsgify.__call__
                             resp = self.call_func(req, *args, **self.kwargs)
                             最终调用本地的wsgi.Router._dispatch,_dispatch返回的app是wsgi.resource对象，
                             内部注册了/test对应的controller router.ControllerTest
                             
                             app调用的封装的__call__最终调用了
                             return resp(environ, start_response) 
                                ->webob.dec.wsgify.__call__, 
                                       ->resp = self.call_func(req, *args, **self.kwargs)
                                          内部调用wsgi.resource对象 调用本地的wsgi.Resource.__call__函数
                                               
                                               ->wsgi.Resource.dispatch
                                                  ->router.ControllerTest.test    调用到想要的controller了
                                               ->return resp(environ, start_response)   
                                                    ->webob.response.__call__
                                               ->回到wsgi.Resource.dispatch
                ->退回到 RoutesMiddleware response = self.app(environ, start_response)的下一条语句
          ->退回到 urlmap __call__ 函数 return app(environ, start_response) 的下一条语句
                
                                   
              
                                
                      
                      
                                                                   
