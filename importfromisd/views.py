#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import socket
import datetime


def index(request):
    return HttpResponse("Сервис работает")


def bos(request):
    # Разбираем получаемую строку на переменные
    # Получаем номер билета
    global pos_name
    media = request.GET.get("MEDIA_NUM", "")
    # Получаем сообщение
    message = request.GET.get("Message", "")
    # Получаем номер турникета
    DeviceCode = request.GET.get("DeviceCode", "")
    # Получаем дату и время
    DateTime = request.GET.get("DateTime", "")
    # Списки турникетов для камер
    Cam01Array = [1, 2, 3]
    Cam02Array = [4, 5, 6]
    Cam03Array = [8, 9, 10]
    Cam04Array = [11, 12, 13]
    # Определяем есть ли Турникет в списке
    if int(DeviceCode) in Cam01Array or int(DeviceCode) in Cam02Array or int(DeviceCode) in Cam03Array or int(
            DeviceCode) in Cam04Array:
        # Если да, то определяем порт и название камеры
        if int(DeviceCode) in Cam01Array:
            UDP_PORT = 2551
            pos_name = "PPS-CAM01 Lift A"
        if int(DeviceCode) in Cam02Array:
            UDP_PORT = 2552
            pos_name = "PPS-CAM02 Lift A"
        if int(DeviceCode) in Cam03Array:
            UDP_PORT = 2555
            pos_name = "PPS-CAM03Lift B"
        if int(DeviceCode) in Cam04Array:
            UDP_PORT = 2556
            pos_name = "PPS-CAM04 Lift B"
        # Распарсиваем строку даты времени
        DateTime = list(DateTime)
        month = ''.join(DateTime[4:6])
        year = ''.join(DateTime[:4])
        day = ''.join(DateTime[6:8])
        date = month + '/' + day + '/' + year
        hour = ''.join(DateTime[9:11])
        minutes = ''.join(DateTime[11:13])
        sec = ''.join(DateTime[13:15])
        time = hour + ':' + minutes + ':' + sec
        text = b"<?xml version=\"1.0\" encoding=\"utf-8\"?><transaction><event_type>POSNG_ACTION</event_type><operation_id>" + date.encode(
            'utf-8') + b"_"+time.encode('utf-8') + b"</operation_id><cashier>Rosa Khutor</cashier><date>" + date.encode(
            'utf-8') + b"</date><time>" + time.encode(
            'utf-8') + b"</time><position></position><quantity></quantity><weight></weight><price></price><article></article><barcode>" + media.encode(
            'utf-8') + b"</barcode><text>[Gate #" + DeviceCode.encode('utf-8') + b"] - " + media.encode(
            'utf-8') + b" - " + message.encode(
            'utf-8') + b"</text><location>" + pos_name.encode('utf-8') + b"</location></transaction>"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.130.131.60", UDP_PORT))

            s.send(text)
            s.close()
        except Exception as e:
            print(e)
        print("Good " + time)
    else:
        print("bad")

    return HttpResponse(media)
