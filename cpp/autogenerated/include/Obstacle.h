#pragma once

#include "ObstacleInterface.h"


namespace comm
{
    class Obstacle : public ObstacleInterface
    {
        public:
            Obstacle() {

            }
            // Accessors
            float get_x(){
                return other / 0.1;
            };
float get_y(){
                return other / 0.1;
            };
float get_width(){
                return other / 0.1;
            };
float get_height(){
                return other / 0.1;
            };

void set_x(float other){
                _x = other * 0.1;
            };
void set_y(float other){
                _y = other * 0.1;
            };
void set_width(float other){
                _width = other * 0.1;
            };
void set_height(float other){
                _height = other * 0.1;
            };

            
            // Serializers
            

            
            
    };
} // namespace comm
