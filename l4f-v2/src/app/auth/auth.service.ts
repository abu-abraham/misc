import { Injectable, NgZone } from '@angular/core';
import { Router } from '@angular/router';
import * as hello from 'hellojs/dist/hello.all.js';

import { Configs } from '../shared/config';

@Injectable()
export class AuthService {
  constructor(
    private zone: NgZone,
    private router: Router
  ) { }

  initAuth() {
      console.log(window.location.href);
    hello.init({
        msft: {
          id: Configs.appId,
          oauth: {
            version: 2,
            auth: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
          },
          scope_delim: ' ',
          form: false
        },
      },
      { redirect_uri: window.location.href }
    );
  }

  login() {
      return new Promise ((resolve, reject)=> {
        hello('msft').login({ scope: Configs.scope }).then(
            () => {
                resolve();
            },
            e => reject(e)
          );
      })
    
  }

  logout() {
    hello('msft').logout().then(
      () => window.location.href = '/',
      e => console.error(e.error.message)
    );
  }
}