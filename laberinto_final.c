#include <stdio.h>
#include <stdlib.h>

// Fución que lee un archivo.
// crea_arreglo: int[] -> int
// Recibe un arreglo de enteros que representan coordenadas, lee un archivo y pasa los datos al arreglo.
// Devuelve un entero que representa cuantos elementos hay en el arreglo.
int crea_coordenadas(int coordenadas[44]) {

  FILE*archivo = fopen("coordenadas.txt", "r"); //abre el archivo en modo solo lectura

  int i=0; //cuenta cuantos elementos hay en el arreglo.
  while (!feof(archivo) && i < 44) {
    fscanf(archivo,"%d", &coordenadas[i]);
    i++;
  }

  fclose(archivo);

  return i-1; //Menos uno ya que el arreglo me lo devuelve con un 0 final.
}

// Función que se fija que las coordenadas estén dentro del laberinto.
// se_pueden_coordenadas: int[],int, int -> int
// Recibe un arreglo de números que representa las coordenadas y dos enteros que representan
//el alto y el ancho del laberinto.
// Dada las coordenadas, las filas y las columnas, se fija que todas las coordenadas
//estén dentro del laberinto, devuelve 0 si se puede y 1 si no.
int se_pueden_coordenadas(int coordenadas[44], int cantidad_coordenadas, int ALTO, int ANCHO) {

  int i;
  int bandera = 0;
    for(i=2; i<cantidad_coordenadas && !bandera; i++) {
      if (i%2 == 0){
        if (coordenadas[i] >= ALTO) {
          bandera =1;
        }
      }
      else{
        if (coordenadas[i] >= ANCHO) {
          bandera = 1;
        }
      }
    }
  return bandera;
  }

// Función que se fija si hay números negativos en el arreglo.
// hay_negativos: int[], int -> int
// Recibe un arreglo de números que representan coordenadas y un número que representa la cantidad
//de elementos que hay en el arreglo. Dada las coordenadas, se fija si hay algún número negativo,
//devolviendo 1 en ese caso. Si no, devuelve un 0.
int hay_negativos(int coordenadas[44], int cantidad_coordenadas) {

  int i;
  int bandera = 0;
  for(i=0; i < cantidad_coordenadas && !bandera  ; i++) {
    if (coordenadas[i] < 0) {
      bandera = 1;
    }
  }
  return bandera;
}


// Función que coloca las casillas vacias en el laberinto.
// colocar_vacios: int[][], int, int -> None
// Recibe un arreglo de enteros que representa el laberinto y entereos que representan
//el ancho y el largo del laberinto. En base a eso va a llenar todo de casillas vacías.
void colocar_vacios(int laberinto[][15], int ALTO, int ANCHO) {

  int i,j;
  int contador = 1;
  for(i=0; i<ALTO; i++) {
    for(j=0; j<ANCHO; j++) {
      laberinto[i][j] = 0;
    }
  }
}



// Función que coloca las paredes en el laberinto.
// colocar_paredes: int[], int[][], int -> None
// Función que recibe un arreglo de enteros que representa coordenadas, un arreglo de arreglo de enteros
//que representa el laberinto y un número entero que representa la cantidad de coordenadas.
void colocar_paredes(int coordenadas[44], int laberinto[][15], int cantidad_coordenadas) {

  int i=4 ;//índices de las coordenadas
  while(i<cantidad_coordenadas) {
    if (laberinto[coordenadas[i]][coordenadas[i+1]] != 2){ //si no está el objetivo
        laberinto[coordenadas[i]][coordenadas[i+1]] = 1;  //se coloca la pared
        i=i+2;
    }
    else{
      i=i+2;
    }
  }
}

void crea_laberinto(int laberinto[][15], int ALTO, int ANCHO){
  //Función que crea el archivo con el laberinto
  // crea_laberinto: int[][], int, int -> None
  // Recibe un arreglo de arreglo de enteros que representa el laberinto y dos entereos
  //que representan el alto y el ancho del laberinto, y crea un archivo con el laberinto.

	FILE* archivo = fopen("laberinto.txt", "w"); //w:solo escritura

  int f=0; //filas
  while (f < ALTO) {
    int c=0; //columnas
    while (c < ANCHO){
      while(c < ANCHO-1){
        fprintf(archivo,"%d", laberinto[f][c]);
        c++;
      }
      fprintf(archivo,"%d\n", laberinto[f][c]);
      c++;
    }
    f++;
  }
  fclose (archivo);
}



//Función principal.
//Lee un archivo de coordenadas y devuelve un archivo (si se puede) con números que
//representan un laberinto. No se va a poder crear el archivo de texto cuando haya números
//negativos en las coordenadas, cuando se quieran poner paredes en coordenadas mayores al tamaño
//del laberinto o cuando no haya verdaderamente un grupo de coordenadas.
int main(){

  int coordenadas[44];
  int laberinto[15][15];
  int cantidad_coordenadas = crea_coordenadas(coordenadas);

  int ANCHO = coordenadas[1];
  int ALTO = coordenadas[0];
  int objetivo_f = coordenadas[2];
  int objetivo_c = coordenadas[3];

  if (hay_negativos(coordenadas, cantidad_coordenadas)) {
    printf("El archivo posee números negativos.\n");
  }
  else{
    if (se_pueden_coordenadas(coordenadas,cantidad_coordenadas, ALTO, ANCHO)) {
      printf("Las coordenadas del objetivo no son posibles.\n");
    }
    else{
      if  (cantidad_coordenadas%2 != 0) {
        printf("El archivo no posee coordenadas completas.\n");
      }
      else {
        colocar_vacios(laberinto, ALTO, ANCHO);
        laberinto[objetivo_f][objetivo_c] = 2;  //se coloca el objetivo en el laberinto.
        colocar_paredes(coordenadas, laberinto, cantidad_coordenadas);
        crea_laberinto(laberinto, ALTO, ANCHO);
        printf("Se creó el laberinto exitosamente.\n");
      }
    }
  }
  return 0;
}
