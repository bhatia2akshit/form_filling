import { Injectable } from '@angular/core';
import { environment } from '../../environments/environments';

@Injectable({providedIn: 'root'})
export class ConfigService {
  readonly apiUrl = environment.backendEndpoint;
  readonly pdfPath = environment.pdfPath;
  readonly jsonPath = environment.jsonPath;
}