import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import en from './i18n/en.json';
import ru from './i18n/ru.json';

@Injectable({ providedIn: 'root' })
export class TranslationService {
  private current = new BehaviorSubject<Record<string, string>>(ru as Record<string,string>);
  private lang = new BehaviorSubject<string>('ru');

  get translations$(): Observable<Record<string,string>> {
    return this.current.asObservable();
  }

  get currentLang$(): Observable<string> {
    return this.lang.asObservable();
  }

  setLang(code: string) {
    this.lang.next(code);
    if (code === 'ru') {
      this.current.next(ru as Record<string,string>);
    } else {
      this.current.next(en as Record<string,string>);
    }
  }

  instant(key: string): string {
    const t = this.current.value;
    return t && t[key] ? t[key] : key;
  }
}
