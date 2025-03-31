import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ConfigService } from './config.service';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {

  constructor(private http: HttpClient, private configParams: ConfigService) { }

  analyzeDocuments(files: File[]): Observable<any> {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file, file.name);
    });

    const backend_url = this.configParams.apiUrl;

    return this.http.post(`${backend_url}/analyze-documents`, formData);
  }

  getJSONDocuments(file: File[]) {
    return ;
  }
}