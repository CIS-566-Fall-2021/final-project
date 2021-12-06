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
    Button clearButton;

    [SerializeField]
    Button quitButton;

    [SerializeField]
    Button helpButton;

    [SerializeField]
    Toggle weightedToggle;

    [SerializeField]
    Toggle drawOutputToggle;

    [SerializeField]
    GameObject popupBackground;

    [SerializeField]
    GameObject errorPopup;

    [SerializeField]
    GameObject helpPopup;

    [SerializeField]
    TMPro.TMP_Dropdown tilemapDropdown;

    [SerializeField]
    ScrollRect tilePalette;

    [SerializeField]
    WaveFunctionCollapse wfc;

    [SerializeField]
    TileBase fallback;

    [SerializeField]
    List<Tilemap> tilemaps;

    [SerializeField]
    List<GameObject> tilePalettes;

    [SerializeField]
    private TileBase tileBrush;

    [SerializeField]
    private Tilemap activeTilemap;

    [SerializeField]
    private Tilemap previewTilemap;

    [SerializeField]
    private Tilemap outputTilemap;

    [SerializeField]
    private Tilemap outputDrawTilemap;

    private Vector3Int previewGridPosition;

    private bool wfcOff = true;

    private bool popupOff = true;

    void Awake() {
        previewGridPosition = Vector3Int.up;
        SetInputTilemap(0);
        ToggleInput(false);
        SwitchOutputDraw(false);    
    }

    void Update() {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Exit();
        }

        if (wfcOff && popupOff)
        {
            if (tileBrush != null)
            {
                Vector2 mousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);

                // let user preview what they draw
                if (previewGridPosition != previewTilemap.WorldToCell(mousePosition))
                {
                    previewTilemap.SetTile(previewGridPosition, null);
                    previewGridPosition = previewTilemap.WorldToCell(mousePosition);
                    if (CheckBounds(activeTilemap, previewGridPosition) || CheckBounds(outputTilemap, previewGridPosition))
                    {
                        previewTilemap.SetTile(previewGridPosition, tileBrush);
                    }
                }

                // draw on input tilemap
                if (Input.GetMouseButton(0))
                {
                    Vector3Int gridPosition = activeTilemap.WorldToCell(mousePosition);
                    if (CheckBounds(activeTilemap, gridPosition) && tileBrush != fallback)
                    {
                        activeTilemap.SetTile(gridPosition, tileBrush);
                    }
                    gridPosition = outputTilemap.WorldToCell(mousePosition);
                    if (outputDrawTilemap.gameObject.activeSelf && CheckBounds(outputTilemap, gridPosition))
                    {
                        if (tileBrush == fallback)
                        {
                            outputDrawTilemap.SetTile(gridPosition, null);
                        }
                        else
                        {
                            outputDrawTilemap.SetTile(gridPosition, tileBrush);
                        }
                    }
                }
            }
        }
    }

    bool CheckBounds(Tilemap target, Vector3Int pos)
    {
        BoundsInt bounds = target.cellBounds;
        return pos.x >= bounds.xMin && pos.x < bounds.xMax && pos.y >= bounds.yMin && pos.y < bounds.yMax;
    }

    public void Exit()
    {
        Application.Quit();
    }

    void ShowPopup()
    {
        popupOff = false;
        popupBackground.SetActive(true);
    }

    public void ShowError(string text)
    {
        TextMeshProUGUI errorText = errorPopup.GetComponentInChildren<TextMeshProUGUI>();
        errorText.text = text;
        ShowPopup();
        errorPopup.SetActive(true);
    }

    public void ShowHelp()
    {
        ShowPopup();
        helpPopup.SetActive(true);
    }

    public void ClosePopups()
    {
        popupOff = true;
        popupBackground.SetActive(false);
        errorPopup.SetActive(false);
        helpPopup.SetActive(false);
    }

    public void SetBrush(TileBase tile)
    {
        tileBrush = tile;
    }
    
    public void ToggleInput(bool val)
    {
        wfcOff = val;
        calculateButton.interactable = val;
        clearButton.interactable = val;
        quitButton.interactable = val;
        helpButton.interactable = val;
        weightedToggle.interactable = val;
        drawOutputToggle.interactable = val;
        tilemapDropdown.interactable = val;
    }

    public void SetInputTilemap(int tilemap)
    {
        if (tilemap >= tilemaps.Count)
        {
            return;
        }
        activeTilemap = tilemaps[tilemap];
        tileBrush = null;
        outputDrawTilemap.ClearAllTiles();
        wfc.SetInputTilemap(tilemaps[tilemap]);
        wfc.ClearOutput();
        SwitchTilemaps(tilemap);
    }

    void SwitchTilemaps(int target)
    {
        for (int i = 0; i < tilemaps.Count; i++)
        {
            if (i == target)
            {
                tilemaps[i].gameObject.SetActive(true);
                tilePalettes[i].SetActive(true);
            }
            else
            {
                tilemaps[i].gameObject.SetActive(false);
                tilePalettes[i].SetActive(false);
            }
        }
        tilePalette.content = tilePalettes[target].GetComponent<RectTransform>();
    }

    public void SwitchOutputDraw(bool val)
    {
        outputDrawTilemap.gameObject.SetActive(val);
    }
}
