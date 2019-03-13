import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RequestsService {

  constructor(private http: HttpClient) { }

  public get(url: string): Promise<any>{
    return new Promise((resolve, reject)=> {
      this.http.get(url).subscribe((data) => { 
            resolve(data);
        } ,(error) => {
            reject(error);
        });
    });
  }

  public post(url: string, body :any ){
    return new Promise((resolve, reject)=> {
      this.http.post(url, body).subscribe((data) => { 
          resolve(data);
      } ,(error) => {
          reject(error);
      });
    });
  }
}