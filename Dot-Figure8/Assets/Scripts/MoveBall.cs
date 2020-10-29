using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveBall : MonoBehaviour
{
    // private vector
    private Vector3 startPos;

    // member variables
    private float speed = 2;
    private float xScale = 6;
    private float yScale = 3;

    void Start () 
    {   
        //get starting position
        startPos = transform.position;
    }

    void Update ()
    {   
        //move ball
        transform.position = startPos + (Vector3.right * Mathf.Sin(Time.timeSinceLevelLoad/2*speed)*xScale - Vector3.up * Mathf.Sin(Time.timeSinceLevelLoad * speed)*yScale);
    }
}
