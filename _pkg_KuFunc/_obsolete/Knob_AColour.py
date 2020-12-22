'''

backup file for Knob_AColour in HoverValue

'''


class Knob_AColour(QtWidgets.QWidget):
	def __init__(self, nuke_knob=''):
		super(Knob_AColour, self).__init__()

		# Instance ID
		self.nuke_knob = nuke_knob
		self.Class = 'Knob_AColour'

		# Instance properties

		# widgets

		# group slider
		self.slider_box = Knob_EditBox(self.nuke_knob)
		self.slider_slider = Knob_Slider(self.nuke_knob)

		self.slider_box.valueChanged.connect(self.onChanged_slider)
		self.slider_slider.valueChanged.connect(self.onChanged_slider)

		self.sets_slider = Knob_Sets()
		self.sets_slider.add_widgets(self.slider_box, self.slider_slider)

		# group editbox
		self.editbox_r = Knob_EditBox(self.nuke_knob)
		self.editbox_r.setStyleSheet("QDoubleSpinBox {border: 1px solid darkred}")
		self.editbox_g = Knob_EditBox(self.nuke_knob)
		self.editbox_g.setStyleSheet("QDoubleSpinBox {border: 1px solid darkgreen}")
		self.editbox_b = Knob_EditBox(self.nuke_knob)
		self.editbox_b.setStyleSheet("QDoubleSpinBox {border: 1px solid darkblue}")
		self.editbox_a = Knob_EditBox(self.nuke_knob)
		self.editbox_a.setStyleSheet("QDoubleSpinBox {border: 1px solid gray}")

		self.editbox_r.valueChanged.connect(self.onChanged_editboxes)
		self.editbox_g.valueChanged.connect(self.onChanged_editboxes)
		self.editbox_b.valueChanged.connect(self.onChanged_editboxes)
		self.editbox_a.valueChanged.connect(self.onChanged_editboxes)

		self.sets_editboxes = Knob_Sets()
		self.sets_editboxes.add_widgets(self.editbox_r, self.editbox_g, self.editbox_b, self.editbox_a)

		# swap button
		self.btn_swap = QtWidgets.QPushButton('4')
		self.btn_swap.setCheckable(True)
		self.btn_swap.clicked.connect(self.onClicked)
		self.btn_swap.toggled.connect(self.onToggle)
		self.btn_swap.setFixedWidth(WIDGET_HEIGHT)


		# layout
		self.sets_swap = Knob_Sets()
		self.sets_swap.add_widgets(self.sets_slider, self.sets_editboxes)

		self.layout = QtWidgets.QHBoxLayout()
		self.layout.setContentsMargins(0,0,0,0)
		self.setLayout(self.layout)
		self.layout.addWidget(self.sets_swap)
		self.layout.addStretch()
		self.layout.addWidget(self.btn_swap)

		self.setDefaults()

	def setDefaults(self):
		'''both sets are hidden on instancing'''
		self.sets_editboxes.hide()
		# self.sets_slider.hide()
		knob_resize(self)

	def onToggle(self):
		'''hide widget and value transfer between two sets of widgets'''
		_sender = self.sender()
		_state = _sender.isChecked()

		if _state == True:
			self.sets_slider.hide()
			self.sets_editboxes.show()
			knob_resize(self)
		elif _state == False:
			self.sets_editboxes.hide()
			self.sets_slider.show()
			knob_resize(self)
		
	def onClicked(self):
		'''user clicked on the button'''
		_sender = self.sender()
		_state = _sender.isChecked()
		_v_out = self.value_transfer(_state)
		set_nuke_knob(self, self.nuke_knob, _v_out)

	def set_range(self, min, max):
		'''set range for slider'''
		_precision = self.slider_slider.PRECISION
		self.slider_slider.setRange(min*_precision, max*_precision)

	def set_value(self, v):
		'''called when instancing'''

		print self.nuke_knob

		if isinstance(v, list):
			self.btn_swap.setChecked(True)
			self.editbox_r.set_value(v[0])
			self.editbox_g.set_value(v[1])
			self.editbox_b.set_value(v[2])
			self.editbox_a.set_value(v[3])
			self.slider_slider.set_value(rgb2luma(v))
			print 'slider - hidden', self.slider_slider.get_value()
		else:
			self.btn_swap.setChecked(False)
			self.slider_slider.set_value(v)
			self.editbox_r.set_value(v)
			self.editbox_g.set_value(v)
			self.editbox_b.set_value(v)
			self.editbox_a.set_value(v)
			print 'editboxes - hidden', [self.editbox_r.get_value(),self.editbox_g.get_value(),self.editbox_b.get_value(),self.editbox_a.get_value()]
			# slider_editbox change value when slider_slider changes value

	def onChanged_slider(self):
		'''when editbox or slider is edited and change each other values'''
		_sender = self.sender()
		_v = _sender.get_value()

		if isinstance(_sender, Knob_Slider):
			self.slider_box.set_value(_v)
		elif isinstance(_sender, Knob_EditBox):
			self.slider_slider.set_value(_v)

		# double secure prevent recursion on instance
		if self.btn_swap.isChecked() == False: # show slider
			self.value_transfer(False)
			set_nuke_knob(self, self.nuke_knob, _v)
	
	def onChanged_editboxes(self):
		'''when editboxes value is cahnged'''
		_nuke_value = get_nuke_value(self, self.nuke_knob)
		_sender = self.sender()
		global value_out

		if not isinstance(_nuke_value, float):
			if _sender is self.editbox_r:
				_nuke_value[0] = _sender.get_value()
				value_out = _nuke_value
			elif _sender is self.editbox_g:
				_nuke_value[1] = _sender.get_value()
				value_out = _nuke_value
			elif _sender is self.editbox_b:
				_nuke_value[2] = _sender.get_value()
				value_out = _nuke_value
			elif _sender is self.editbox_a:
				_nuke_value[3] = _sender.get_value()
				value_out = _nuke_value
		
		# double secure prevent recursion on instance
		if self.btn_swap.isChecked() == True: # show editboxes
			self.value_transfer(True)
			set_nuke_knob(self, self.nuke_knob, value_out)

	def value_transfer(self, state):
		'''transfer value when knobs are swapped
		@state: (bool) state of the button, checked or not-checked
		return: (float or list of float) value depends on checked state
		'''

		global value_out

		if state == True:
			_v = [self.editbox_r.get_value(),self.editbox_g.get_value(),self.editbox_b.get_value(),self.editbox_a.get_value()]
			
			self.slider_slider.set_value(rgb2luma(_v))

			value_out = _v
		
		elif state == False:
			_v = self.slider_box.get_value()

			self.editbox_r.set_value(_v)
			self.editbox_g.set_value(_v)
			self.editbox_b.set_value(_v)
			self.editbox_a.set_value(_v)
			
			value_out = _v

		return value_out