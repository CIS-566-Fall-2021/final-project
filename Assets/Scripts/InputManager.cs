using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;
using UnityEngine.UI;
using TMPro;

public class InputManager : MonoBehaviour
{
    [SerializeField]
    Button calculateButton;
    [SerializeField]
    Toggle weightedToggle;
    [SerializeField]
    TMPro.TMP_Dropdown tilemapDropdown;

    [SerializeField]
    WaveFunctionCollapse wfc;

    [SerializeField]
    List<Tilemap> tilemaps;
    

    void Awake() {
        SetInputTilemap(0);
        ToggleInput(false);    
    }

    void Update() {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Exit();
        }    
    }

    public void Exit()
    {
        Application.Quit();
    }
    
    public void ToggleInput(bool val)
    {
        calculateButton.interactable = val;
        weightedToggle.interactable = val;
        tilemapDropdown.interactable = val;
    }

    public void SetInputTilemap(int tilemap)
    {
        if (tilemap >= tilemaps.Count)
        {
            return;
        }
        wfc.SetInputTilemap(tilemaps[tilemap]);
        SwitchTilemaps(tilemaps[tilemap]);
    }

    void SwitchTilemaps(Tilemap target)
    {
        foreach (Tilemap t in tilemaps)
        {
            if (t.Equals(target))
            {
                t.gameObject.SetActive(true);
            }
            else
            {
                t.gameObject.SetActive(false);
            }
        }
    }
}
