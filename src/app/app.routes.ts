import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home').then((m) => m.Home),
  },
  {
    path: 'cardapiodigital',
    loadComponent: () => import('./cardapio/cardapio').then((m) => m.Cardapio),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
