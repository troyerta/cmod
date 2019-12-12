#ifndef D_LedDriver_H
#define D_LedDriver_H
#include <stdint.h>

#define TRUE 1
#define FALSE 0
typedef int BOOL;


void LedDriver_Create(uint16_t * ledsAddress, BOOL activeHigh);
void LedDriver_Destroy(void);

void LedDriver_TurnOn(int ledNumber);
void LedDriver_TurnOff(int ledNumber);
void LedDriver_TurnAllOn(void);
void LedDriver_TurnAllOff(void);
BOOL LedDriver_IsOn(int ledNumber);
BOOL LedDriver_IsOff(int ledNumber);
#endif  /* D_LedDriver_H */

/*
 * Intermediate examples below this comment
 */

#if 0
#ifndef D_LedDriver_H
#define D_LedDriver_H

void LedDriver_Create(void);
void LedDriver_Destroy(void);

#endif  /* D_LedDriver_H */

#if 0
#ifndef D_LedDriver_H
#define D_LedDriver_H
void LedDriver_Create(void);
void LedDriver_Destroy(void);
void LedDriver_TurnOn(int ledNumber);
void LedDriver_TurnOff(int ledNumber);
#endif


#endif  /* D_LedDriver_H */


#endif