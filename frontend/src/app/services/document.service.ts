import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ConfigService } from './config.service';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  readonly backend_url: any;


  constructor(private http: HttpClient, private configParams: ConfigService) {
    this.backend_url = configParams.apiUrl;
  }


  analyzeDocuments(files: File[]): Observable<any> {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file, file.name);
    });

    return this.http.post(`${this.backend_url}/analyze-documents`, formData);
  }

  getCombinedJson(): Observable<any> {
    return this.http.get(`${this.backend_url}/get-combine-info`);
  }
}
