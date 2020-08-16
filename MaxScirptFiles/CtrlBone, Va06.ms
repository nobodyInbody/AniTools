-- 2019-02-17 : 맥스 2018에서 한글 이름에 문제가 생겨 수정
macroscript CtrlBoneConstraint category:"_AniSeoHyun"
icon:#("Maintoolbar", 9)
(
-- 
--2019-03-27
--2019-05_31 Va06 ing
--VersionText = "CtrlBone Va06 셋팅적용"
VersionText = "CtrlBone Va07 ui와 구조 개선"
--	struct 이름 수정
struct SEO_CtrlBone
(
    boneObj = #(),
    posItems = #(),
    posItemNames = #(),
    rotItems = #(),
	rotItemNames = #(),
	EnableRotLink = true,

    fn checkIsConstraint obj =
    (
        local _bool = false
        local _ctrlPos = undefined
        local _ctrlRot = undefined
        if (classof obj.controller == prs)  do
        (
            _ctrlPos = obj.pos.controller
            _ctrlRot = obj.rotation.controller
        )
        if (classOf _ctrlPos == Position_Constraint) do
        (
            _bool = true
        )
        if (classOf _ctrlRot == Orientation_Constraint) do
        (
            _bool = true
        )
        _bool --return
    ),
    fn getCtrlTargets ctrl =
    (
        local _nTemp = 0
        if (classOf ctrl == Position_Constraint) or (classOf ctrl == Orientation_Constraint) do
        (
            _nTemp = ctrl.getNumTargets()
        )
        _nTemp
    ),
    fn findPos obj =
    (
        local _ctrl = obj.pos.controller
        local _nTemp = getCtrlTargets _ctrl
        local _vTemps = #()
        local _sTemps = #()
        for i = 1 to _nTemp do
        (
            local _obj = _ctrl.getNode i
            append _vTemps _obj
            append _sTemps _obj.name
        )
        append posItems _vTemps
        append posItemNames _sTemps
    ),
    fn findRot obj =
    (
        local _ctrl = obj.rotation.controller
        local _nTemp = getCtrlTargets _ctrl
        local _vTemps = #()
        local _sTemps = #()
        for i = 1 to _nTemp do
        (
            local _obj = _ctrl.getNode i
            append _vTemps _obj
            append _sTemps _obj.name
        )
        append rotItems _vTemps
        append rotItemNames _sTemps
    ),
    fn boneObjCount =
    (
        boneObj.count
    ),
    fn posSetNum _ctrl valNum val =
    (
        local _nTemp = getCtrlTargets _ctrl
        local _valNum = valNum
        for i = 1 to _nTemp do
        (
            if i == _valNum then
            (
                _ctrl.setWeight i val
            )
            else _ctrl.setWeight i 0
        )
    ),
    fn setWeightNum _ctrl valNum val =
    (
		local _nTemp = getCtrlTargets _ctrl
        local _valNum = valNum
        for i = 1 to _nTemp do
        (
            if i == _valNum then
            (
                _ctrl.setWeight i val
            )
            else _ctrl.setWeight i 0
        )
	),
    fn findCurrentRosItem obj =
    ( -- _objNum = i
        local _ctrl = obj.rotation.controller
        local _nTemp = getCtrlTargets _ctrl
        local _objNum = 0
        for i = 1 to _nTemp do
        (
            if (_ctrl.getWeight i) == 100 do
            (
                _objNum = i
            )
        )
        _objNum
    ),
    fn findCurrentPosItem obj =
    ( -- _objNum = i
        local _ctrl = obj.pos.controller
        local _nTemp = getCtrlTargets _ctrl
        local _objNum = 0
        for i = 1 to _nTemp do
        (
            if (_ctrl.getWeight i) == 100 do
            (
                _objNum = i
            )
        )
        _objNum
    ),
    fn setting objs =
    (
        for obj in objs do
        (
            if (checkIsConstraint obj) do
            (
                append boneObj obj
            )
        )
		for obj in boneObj do
		(
			findRot obj
			findPos obj
		)
    )
)-- SEO_CtrlBone End
(  --SHyun_MakeCtrlBone
    local m_mainBone = undefined
    local m_targetBoneRolloutList = #()
    rollout SHyun_MakeCtrlBone "컨스트래인본 연결하기"
    (
        label labelMainBone "" tooltip:"컨스트레인본으로 만들 대상입니다."
        pickbutton btn_목록추가_  "추가하기" across:2 tooltip:"오브젝트(물체)를 선택하여 목록에 추가합니다."
        button btn_목록제거_  "목록제거" tooltip:"목록에서 선택한 항목을 제거합니다."    
        button btn_make "연결하기" tooltip:"목록을 컨스트레인본에 연결합니다"
        listbox tempList "연결대상들" items:#()

        on btn_목록추가_ picked obj do
        (
            append m_targetBoneRolloutList obj
            --print m_targetBoneRolloutList
            tempList.items = for o in m_targetBoneRolloutList collect o.name
        )
        on btn_목록제거_ pressed do
        (
            local selectNum = tempList.selection
            deleteItem m_targetBoneRolloutList selectNum
            tempList.items = for o in m_targetBoneRolloutList collect o.name
        )
        on btn_make pressed do
        (
            --print m_mainBone
            local posCtrl = Position_Constraint()
            m_mainBone.pos.controller = posCtrl
            posConstraintInterface = posCtrl.constraints
            for obj in m_targetBoneRolloutList do (
                posConstraintInterface.appendTarget obj 0
            )
            local rotCtrl = Orientation_Constraint()
            m_mainBone.rotation.controller = rotCtrl
            rotConstraintInterface = rotCtrl.constraints
            for obj in m_targetBoneRolloutList do (
                rotConstraintInterface.appendTarget obj 0
            )
            DestroyDialog SHyun_MakeCtrlBone
        )
        on SHyun_MakeCtrlBone open do
        (
            if selection.count == 1 then (
                m_mainBone = $
                m_targetBoneRolloutList = #()
                tempList.items = m_targetBoneRolloutList
                labelMainBone.text = m_mainBone.name
            )
            else (
                messageBox "만들본을 하나만 선택해주세요."
                DestroyDialog SHyun_MakeCtrlBone
            )
        )
    )
)--SHyun_MakeCtrlBone End
        
(
    if UICtrlboneWindwos != undefined do
    (
        DestroyDialog UICtrlboneWindwos
    )
    _ctrlbone = SEO_CtrlBone()
    fn UIUpDate =
    (
        UICtrlboneWindwos.bonePosList1.selection  = _ctrlbone.findCurrentPosItem _ctrlbone.boneObj[1]
        UICtrlboneWindwos.boneRotList1.selection  = _ctrlbone.findCurrentRosItem _ctrlbone.boneObj[1]
        --print "test"
    )
    rollout UICtrlboneWindwos  ("Ctrlbone" + VersionText )
    (
        button btnMakeBone "생성창" width:75 offset:[0, 0] across:3 align:#center
		button btnReset "리셋" width:75 offset:[0, 0] 
		checkbox btnRotLink "회전값까지" checked:true
        button btnSelectBone "선택" width:75 offset:[0, 0] across:3
        dropdownlist bonePosList1 "" items:#()
        button btnSelectPoslistitem1 "을 선택" 
        label btnTemp1 "Rot" width:75 offset:[0, 0] across:3
        dropdownlist boneRotList1 "" items:#()
        button btnSelectRotlistitem1 "을 선택" 

        on UICtrlboneWindwos open do
        (
			_ctrlbone = SEO_CtrlBone()
			if (_ctrlbone.enableRotLink) do UICtrlboneWindwos.boneRotList1.enabled = false
			_ctrlbone.boneObj = #()
            for obj in selection do
            (
				_ctrlbone.setting obj
            )
            if _ctrlbone.boneObj[1] == undefined then
            (
                --messageBox "컨트롤본셋팅이 없습니다." beef:false
                --DestroyDialog UICtrlboneWindwos
            )
            else
            (
                btnSelectBone.text = _ctrlbone.boneObj[1].name
				bonePosList1.items = _ctrlbone.posItemNames[1]
				btnTemp1.text = (_ctrlbone.boneObj[1].rotation.controller) as string
                boneRotList1.items = _ctrlbone.rotItemNames[1]
                UIUpDate()
            )
            registerTimeCallback UIUpDate
        )
        on UICtrlboneWindwos close do
        (
            unRegisterTimeCallback UIUpDate
        )
        on btnMakeBone pressed do
        (
            if SHyun_MakeCtrlBone != undefined do (
                DestroyDialog SHyun_MakeCtrlBone
            )
            createDialog SHyun_MakeCtrlBone width:150
		)
        on btnReset pressed do
        (
            DestroyDialog UICtrlboneWindwos
            createDialog UICtrlboneWindwos width:350 pos:(mouse.screenpos - [175,45])
		)
		on btnRotLink changed state do
		(
			if state then
			(
				_ctrlbone.EnableRotLink = true
				bonePosList1.enabled  = false
			)
			else
				(
					_ctrlbone.EnableRotLink = false
					bonePosList1.enabled  = true
				)
		)
        on btnSelectBone pressed do
        (
            try
            (
                select _ctrlbone.boneObj[1]
            )
            catch ( print "boneOjb이 없습니다.")
        )
        on bonePosList1 selected i do
        (
			local _posCtrl = (_ctrlbone.boneObj[1]).pos.controller
			_ctrlbone.setWeightNum _posCtrl i 100
			-- Va05 회전값을 같이 제어하는 부분
			if _ctrlbone.EnableRotLink = true do
				(
					local _rotCtrl = (_ctrlbone.boneObj[1]).rotation.controller
					local rotTargetObj = _rotCtrl.getNode i
					local potTargetObj = _posCtrl.getNode i
					if (rotTargetObj.name == potTargetObj.name ) do 
					(
						_ctrlbone.setWeightNum _rotCtrl i 100
					)
					boneRotList1.selection = i
				)
        )
        --
        on btnSelectPoslistitem1 pressed do
        (
            try
            (
                local _num = bonePosList1.selection
                select _ctrlbone.posItems[1][_num]
            ) catch (            )
		)
        on boneRotList1 selected i do
		(
			local _rotCtrl = (_ctrlbone.boneObj[1]).rotation.controller
			_ctrlbone.setWeightNum _rotCtrl i 100
		)
        on btnSelectRotlistitem1 pressed do
		(
            try
            (
                local _num = boneRotList1.selection
                select _ctrlbone.rotItems[1][_num]
            ) catch (
                local e = getCurrentException()
                format "rotItem이 없음. \n % " e
            )


		)
    )
    createDialog UICtrlboneWindwos width:350 pos:(mouse.screenpos - [175,45])
)
)

