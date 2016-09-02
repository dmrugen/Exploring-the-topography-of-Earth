# -*- coding: utf-8 -*-
"""
The following program accepts the name of a parameter file. It reads the parameter
file, reads the data file and then reads the data. The program then performs 
following tasks - 
    1) Displays the locations (latitudes and longitudes) of the tallest
       peak and the deepest valley.
    2) Plots contour for the given set of data values
    3) Plots elevation slice for the given latitude
    4) Plots elevation slice for the given longitude

Setting to accept the parameter file as a command line argument is made
in Run -> Configure -> General settings

Author: Mrugen Anil Deshmukh (mad5js)

Date created: 1 March 2016
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Function to locate tallest peak
def tallestpeak(data,lat,lon):
    maxalt = np.amax(data)
    maxindices = np.argwhere(data == maxalt)
    valmax = [lat[maxindices[0][0]], lon[maxindices[0][1]]]
    return valmax

# Function to locate deepest point
def deepestland(data, lat, lon):
    minalt = np.amin(data)
    minindices = np.argwhere(data == minalt)
    valmin = [lat[minindices[0][0]], lon[minindices[0][1]]]
    return valmin

# Function returning the elevation slice for a particular latitude 
def latvector(data, latitude, n):
    if any(latitude == n):
        li = np.where(latitude == n)
        index = li[0][0]
        x = data[index, :]
        return x
    else:
        print("\nPlease enter a valid number for latitude")
   
# Function returning elevation slice for a particular longitude
def lonvector(data, longitude, n):
    if any(longitude == n):
        lo = np.where(longitude == n)
        index = lo[0][0]
        x = data[:,index]
        return x
    else:
        print("\nPlease enter a valid number for longitude")
        
def main():
    filename = ''
    parameterfile = sys.argv[1]
    with(open(parameterfile,'r')) as parameter:
        (_,filename) = parameter.readline().strip().split('=') 
        filename = os.path.normpath(filename)
        strlat = float(parameter.readline().strip().split('=')[1])
        strlon = float(parameter.readline().strip().split('=')[1])
        reslat = float(parameter.readline().strip().split('=')[1])
        reslon = float(parameter.readline().strip().split('=')[1])
    with open(filename,'r') as contourdata:
        data = np.loadtxt(contourdata)
    
    # Creating Latitude and Longitude vectors
    latend = -89.751                            # End point for Latitude vector
    lat = np.arange(strlat,latend,-reslat)      # Latitude vector
    lonend = 359.751                            # End point for Longitude vector
    lon = np.arange(strlon,lonend, reslon)      # Longitude vector

    # To display the location of the tallest peak
    x1,y1 = tallestpeak(data,lat,lon)
    print("\nLatitude for tallest peak is",x1,"\nLongitude for tallest peak is",y1)
    
    # To display the location of the deepest valley
    j,k = deepestland(data, lat, lon)
    print("\nLatitude for deepest point is",j,"\nLongitude for deepest point is",k)
    
    # Plotting the contour of given values
    X, Y = np.meshgrid(lon,lat)
    Z = data    
    plt.contourf(X,Y,Z)
    plt.title('CONTOUR OF GIVEN ALTITUDE VALUES')
    plt.xlabel('Longitudes')
    plt.ylabel('Latitudes')
    
    # Plotting the highest point on the contour (green circle)
    ax = plt.subplot(111)
    ax.plot([y1],[x1],'go')
    
    # Plotting the lowest point on the contour (red circle)
    bx = plt.subplot(111)
    bx.plot([k],[j],'ro')
    
    # Plotting the elevation slice for a particular latitude 
    latplot = 38.25                         # Latitude value
    elslice = latvector(data, lat, latplot)
    plt.figure()
    plt.plot(lon, elslice)
    plt.title('Elevation slice for the particular Latitude')
    plt.xlabel('Longitude values corrsponding to the given Latitude')
    plt.ylabel('Altitude values')
    
    # Plotting the elevation slice for a particular longitude
    lonplot = 224.25                        # Longitude value
    lonslice = lonvector(data, lon, lonplot)
    plt.figure()
    plt.plot(lat, lonslice)
    plt.title('Elevation slice for the particular Longitude')
    plt.xlabel('Latitude values corresponding to the given Longitude')
    plt.ylabel('Altitude values')
    
main()
